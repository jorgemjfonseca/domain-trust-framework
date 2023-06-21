import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { LAMBDA } from '../LAMBDA/LAMBDA';
import { BUS } from '../BUS/BUS';
import { STACK } from '../STACK/STACK';

export class WORKFLOW {

    Scope: STACK;
    Super: stepfunctions.StateMachine;
    Name: string;

    public static New(
      scope: STACK, 
      id: string, 
      workflow: STATES,
      props: cdk.aws_stepfunctions.StateMachineProps
    ): WORKFLOW {

        const ret = new WORKFLOW();
        ret.Name = scope.stackName + id;

        ret.Super = new stepfunctions.StateMachine(scope, id,{
          stateMachineName: ret.Name,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          ...props,
        });

        ret.Scope = scope;
        
        // Grant invocation to all lambdas.
        workflow.Lambdas.forEach(fn => 
          ret.InvokesLambda(fn));

        return ret;
    }
    

    public InvokesLambda(fn: LAMBDA): WORKFLOW {
      fn.Super.grantInvoke(this.Super);
      return this;
    }

    
    public Export(alias: string) {
      new cdk.CfnOutput(this.Scope, 'StepFunction', {
        value: this.Super.stateMachineName,
        exportName: alias,
      });
    }


    public TriggeredByBus(
      bus: BUS, 
      // e.g. { source: ["CustomEvent"], detailType: ["CREATE", "UPDATE", "DELETE"] }
      detailType: string
    ): WORKFLOW 
    {
      const ruleName = this.Name + 'ByBus';
      
      const eventRule = new events
        .Rule(this.Scope, ruleName, {
          ruleName: this.Scope.stackName + ruleName, 
          eventPattern: {
            detailType: [ detailType ]
          },
          eventBus: bus.Super
        });

      const dlq = new sqs.Queue(this.Scope, ruleName + 'Dlq');
              
      eventRule.addTarget(new targets.SfnStateMachine(this.Super, {
          deadLetterQueue: dlq, // Optional: add a dead letter queue
          maxEventAge: cdk.Duration.hours(2), // Optional: set the maxEventAge retry policy
          retryAttempts: 3, // Optional: set the max number of retry attempts
      }));

      return this;
    }
}


export class STATES {

    Name: string;
    Scope: STACK;
    FailureCallback: cdk.aws_stepfunctions.State;
    FirstStep: stepfunctions.IChainable;
    LastStep: stepfunctions.INextable;
    LastStepName: string;
    Lambdas: LAMBDA[] = [];

    constructor(scope: STACK, id: string) {
      this.Scope = scope;
      this.Name = id;

      // Success and failure pass through step
      const fail = new sfn.Fail(
        this.Scope, 
        this.Name + ': Execution Failed');

      // Create Failure Queue
      const failureQueue = new sqs.Queue(
        this.Scope, 
        this.Name + ': Step funtion Failure Queue');

      const failureQueueStep = new tasks.SqsSendMessage(
        this.Scope, 
        this.Name + ': Failure Queue', {
          queue: failureQueue,
          messageBody: sfn.TaskInput.fromJsonPathAt("$"),
        }).next(fail);

      const failureCallback = new sfn.Pass(
        this.Scope, 
        this.Name + 'Failure Callback');

      failureCallback.next(failureQueueStep);
      this.FailureCallback = failureCallback;
    }

    public static New(scope: STACK, id: string) {
      return new STATES(scope, id);
    }

    private ToWorkflowStep(
      fn: LAMBDA, 
      onFailure?: cdk.aws_stepfunctions.State
    ): tasks.LambdaInvoke {
      
      const executionFunction = new tasks.LambdaInvoke(
        this.Scope, 
        this.Name + ': ' + fn.Super.functionName, {
          lambdaFunction: fn.Super,
          retryOnServiceExceptions: true,
          outputPath: '$.Payload'
        });

      if (onFailure) {
        executionFunction.addRetry({ errors: ['Failure Exception'], maxAttempts: 1 });
        executionFunction.addCatch(onFailure, {
          resultPath: "$.message.errorMessage"});
      }

      this.Lambdas.push(fn);

      return executionFunction;
    }


    public InvokeLambda(
      fn: LAMBDA
    ): STATES {
      const step = this.ToWorkflowStep(fn);
      this.FirstStep = this.FirstStep ?? step;
      this.LastStep = step;
      this.LastStepName = fn.Super.functionName;
      return this;
    }

    public ThenInvokeLambda(
      fn: LAMBDA
    ): STATES  {
      const step = this.ToWorkflowStep(fn);
      this.LastStep.next(
        new sfn.Choice(fn.Super, 
          this.Name + ': Was '+this.LastStepName+' successfull?')
          .when(
            sfn.Condition.stringEquals('$.processedInput.transactionStatus', 'completed'), 
            step)
          .otherwise(this.FailureCallback)
      );
      this.LastStep = step;
      this.LastStepName = fn.Super.functionName;
      return this;
    }

    public ThenSuccess(): STATES  {
      const succeeded = new sfn.Succeed(this.Scope, 
        this.Name + ': Succeed');
      this.LastStep.next(
        new sfn.Choice(this.Scope, this.Name + ': Was '+this.LastStepName+' successfull?')
          .when(
            sfn.Condition.stringEquals('$.processedInput.transactionStatus', 'completed'), 
            succeeded)
          .otherwise(this.FailureCallback)
      );
      return this;
    }

}


export class EXPRESS extends WORKFLOW {

  public static New(scope: STACK, id: string, workflow: STATES): EXPRESS
  {
    const ret = super.New(scope, id, workflow, {
      definition: workflow.FirstStep,
      stateMachineType: stepfunctions.StateMachineType.EXPRESS,
    })
    return ret;
  }
  
}


export class STANDARD extends WORKFLOW {

  public static New(scope: STACK, id: string, workflow: STATES)
  {
    const ret = super.New(scope, id, workflow, {
      definition: workflow.FirstStep,
      stateMachineType: stepfunctions.StateMachineType.STANDARD,
    })
    return ret;
  }
}

