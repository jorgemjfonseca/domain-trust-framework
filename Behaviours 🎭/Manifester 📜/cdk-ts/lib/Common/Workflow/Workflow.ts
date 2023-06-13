import * as cdk from 'aws-cdk-lib';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { LAMBDA } from '../Lambda/Lambda';
import { BUS } from '../EventBus/EventBus';
import { inherits } from 'util';

export class MACHINE {

    Scope: cdk.Stack;
    Super: stepfunctions.StateMachine;
    Name: string;

    public static New(
      scope: cdk.Stack, 
      id: string, 
      workflow: WORKFLOW,
      props: cdk.aws_stepfunctions.StateMachineProps
    ): MACHINE {

        const ret = new MACHINE();
        ret.Name = scope.stackName + id;

        ret.Super = new stepfunctions.StateMachine(scope, id,{
          stateMachineName: ret.Name,
          ...props,
        });

        ret.Scope = scope;
        
        // Grant invocation to all lambdas.
        workflow.Lambdas.forEach(fn => 
          ret.InvokesLambda(fn));

        return ret;
    }
    

    public InvokesLambda(fn: LAMBDA): MACHINE {
      fn.Super.grantInvoke(this.Super);
      return this;
    }

    
    public Export(alias: string) {
      new cdk.CfnOutput(this.Scope, 'StepFunction', {
        value: this.Super.stateMachineName,
        exportName: alias,
      });
    }


    public TriggeredByEventBus(
      bus: BUS, 
      // e.g. { source: ["CustomEvent"], detailType: ["CREATE", "UPDATE", "DELETE"] }
      eventPattern: events.EventPattern): MACHINE 
    {
      const ruleName = this.Name + 'ByBus';
      
      const eventRule = new events
        .Rule(this.Scope, ruleName, {
          ruleName: this.Scope.stackName + ruleName, 
          eventPattern: eventPattern,
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


export class WORKFLOW {

    Scope: cdk.Stack;
    FailureCallback: cdk.aws_stepfunctions.State;
    FirstStep: stepfunctions.IChainable;
    LastStep: stepfunctions.INextable;
    LastStepName: string;
    Lambdas: LAMBDA[] = [];

    constructor(scope: cdk.Stack) {
      this.Scope = scope;

      // Success and failure pass through step
      const fail = new sfn.Fail(this.Scope, 'Execution Failed');

      // Create Failure Queue
      const failureQueue = new sqs.Queue(this.Scope, 'Step funtion Failure Queue');
      const failureQueueStep = new tasks.SqsSendMessage(this.Scope, 'Failure Queue', {
        queue: failureQueue,
        messageBody: sfn.TaskInput.fromJsonPathAt("$"),
      }).next(fail);

      const failureCallback = new sfn.Pass(this.Scope, 'Failure Callback');
      failureCallback.next(failureQueueStep);
      this.FailureCallback = failureCallback;
    }


    private ToWorkflowStep(
      fn: LAMBDA, 
      onFailure?: cdk.aws_stepfunctions.State
    ): tasks.LambdaInvoke {
      
      const executionFunction = new tasks.LambdaInvoke(this.Scope, fn.Super.functionName, {
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
    ): WORKFLOW {
      const step = this.ToWorkflowStep(fn);
      this.FirstStep = this.FirstStep ?? step;
      this.LastStep = step;
      this.LastStepName = fn.Super.functionName;
      return this;
    }

    public ThenInvokeLambda(
      fn: LAMBDA
    ): WORKFLOW  {
      const step = this.ToWorkflowStep(fn);
      this.LastStep.next(
        new sfn.Choice(fn.Super, 
          'Was '+this.LastStepName+' successfull?')
          .when(
            sfn.Condition.stringEquals('$.processedInput.transactionStatus', 'completed'), 
            step)
          .otherwise(this.FailureCallback)
      );
      this.LastStep = step;
      this.LastStepName = fn.Super.functionName;
      return this;
    }

    public ThenSuccess(): WORKFLOW  {
      const succeeded = new sfn.Succeed(this.Scope, ' Succeed');
      this.LastStep.next(
        new sfn.Choice(this.Scope, 'Was '+this.LastStepName+' successfull?')
          .when(
            sfn.Condition.stringEquals('$.processedInput.transactionStatus', 'completed'), 
            succeeded)
          .otherwise(this.FailureCallback)
      );
      return this;
    }

}


export class EXPRESS extends MACHINE {

  public static New(scope: cdk.Stack, id: string, workflow: WORKFLOW): EXPRESS
  {
    const ret = super.New(scope, id, workflow, {
      definition: workflow.FirstStep,
      stateMachineType: stepfunctions.StateMachineType.EXPRESS,
    })
    return ret;
  }
  
}


export class STANDARD extends MACHINE {

  public static New(scope: cdk.Stack, id: string, workflow: WORKFLOW)
  {
    const ret = super.New(scope, id, workflow, {
      definition: workflow.FirstStep,
      stateMachineType: stepfunctions.StateMachineType.STANDARD,
    })
    return ret;
  }
}

