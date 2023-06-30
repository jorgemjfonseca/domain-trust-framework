import * as appconfig from 'aws-cdk-lib/aws-appconfig';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';
import * as cdk from 'aws-cdk-lib';
import { LAMBDA } from '../LAMBDA/LAMBDA';
import { SQS } from '../SQS/SQS';


export class APPCONFIG extends CONSTRUCT {

    Super: appconfig.CfnApplication;
    private ConfigVersion: appconfig.CfnHostedConfigurationVersion;
    private Environment: appconfig.CfnEnvironment;
    private Profile: appconfig.CfnConfigurationProfile;

    constructor (scope: STACK, app: appconfig.CfnApplication)
    {
      super(scope);
      this.Super = app;
    }

    public static NewJson(scope: STACK, name: string, object: any): APPCONFIG {
      return this.New(scope, 'application/json', name, JSON.stringify(object));
    }

    public static NewYaml(scope: STACK, name: string, data: string): APPCONFIG {
      return this.New(scope, 'application/x-yaml', name, data);
    }

    public static New(scope: STACK, contentType: string, name: string, data: string): APPCONFIG {
      
      const app = new appconfig.CfnApplication(scope, name, {
          name: `${scope.Name}-${name}`,
      });
      
      const ret = new APPCONFIG(scope, app);

      // you can customize this as per your needs.
      const immediateDeploymentStrategy = new appconfig.CfnDeploymentStrategy(
        ret,
        scope.Name+name+"DeployStrategy",
        {
          name: "ImmediateDeployment",
          deploymentDurationInMinutes: 0,
          growthFactor: 100,
          replicateTo: "NONE",
          finalBakeTimeInMinutes: 0,
        }
      );

      // setup an app config env
      ret.Environment = new appconfig.CfnEnvironment(
        ret,
        scope.RandomName(scope.Name+name+"Env"),
        {
          applicationId: app.ref,
          name: "Dev",
        }
      );

      // setup config profile
      ret.Profile = new appconfig.CfnConfigurationProfile(
        ret,
        scope.RandomName(scope.Name+name+"Profile"),
        {
          name: scope.Name+name+"Profile",
          applicationId: app.ref,
          // we want AppConfig to manage the configuration profile, unless we need from SSM or S3.
          locationUri: "hosted",
          // This can also be "AWS.AppConfig.FeatureFlags"
          type: "AWS.Freeform",
        }
      );

      // Update AppConfig
      ret.ConfigVersion = new appconfig.CfnHostedConfigurationVersion(
        ret,
        scope.RandomName("HostedConfigurationVersion"),
        {
          applicationId: app.ref,
          configurationProfileId: ret.Profile.ref,
          content: data,
          // https://www.rfc-editor.org/rfc/rfc9110.html#name-content-type
          contentType: contentType,
        }
      );
      
      // Perform deployment.
      new appconfig.CfnDeployment(ret, 
        scope.RandomName("Deployment"), {
          applicationId: app.ref,
          configurationProfileId: ret.Profile.ref,
          configurationVersion: ret.ConfigVersion.ref,
          deploymentStrategyId: immediateDeploymentStrategy.ref,
          environmentId: ret.Environment.ref,
        });

      return ret;
    }


    // 👉 https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions-about-predefined-notification-eventbridge.html
    public static PublishToEventBridge(stack: STACK, appConfigArn: string) {
      // Send events to event bridge
      new appconfig.CfnExtensionAssociation(stack, "Association", {
        extensionIdentifier: 'AWS.AppConfig.DeploymentNotificationsToEventBridge',
        resourceIdentifier: appConfigArn
      });
    }
    public PublishToEventBridge(): APPCONFIG  {
      APPCONFIG.PublishToEventBridge(this.Scope, this.Super.ref);
      return this;
    }

    // 👉 https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions-about-predefined-notification-sqs.html
    public static PublishToSQS(stack: STACK, appConfigArn: string, sqs: SQS) {
      return new appconfig.CfnExtensionAssociation(stack, "Association", {
        extensionIdentifier: 'AWS.AppConfig.DeploymentNotificationsToSqs',
        resourceIdentifier: appConfigArn,
        parameters: {
          queueArn: sqs.Super.queueArn
        }
      });
    }
    public PublishToSQS(sqs: SQS): APPCONFIG  {
      const extension = APPCONFIG.PublishToSQS(this.Scope, this.Super.ref, sqs);
      this.Scope.Export('AppConfigToSQS', extension.ref);
      return this;
    }


    public AddEnvironment(fn: LAMBDA): APPCONFIG {
      fn.AddEnvironment('CONFIG_APP', this.Super.name);
      fn.AddEnvironment('CONFIG_APP_ID', this.ConfigVersion.applicationId);
      fn.AddEnvironment('CONFIG_ENV', this.Environment.name);
      fn.AddEnvironment('CONFIG_PROFILE', this.Profile.name);
      return this;
    }

    public static ImportArn(alias: string): string {
      return cdk.Fn.importValue(alias + 'ApplicationArn');
    }

    public static ImportName(alias: string): string {
      return cdk.Fn.importValue(alias + 'Application');
    }

    public static ImportRef(alias: string): string {
      return cdk.Fn.importValue(alias + 'ApplicationRef');
    }

    public Export(alias: string): APPCONFIG {
      
      new cdk.CfnOutput(this.Super, alias + 'Application', {
        value: this.Super.name,
        exportName: alias + 'Application',
      });

      new cdk.CfnOutput(this.Super, alias + 'ApplicationId', {
        value: this.ConfigVersion.applicationId,
        exportName: alias + 'ApplicationId',
      });

      new cdk.CfnOutput(this.Super, alias + 'ApplicationRef', {
        value: this.Super.ref,
        exportName: alias + 'ApplicationRef',
      });

      new cdk.CfnOutput(this.Super, alias + 'ApplicationArn', {
        exportName: alias + 'ApplicationArn',
        value: `arn:aws:appconfig:${this.Scope.region}:${this.Scope.account}:application/${this.Super.ref}`
      });

      new cdk.CfnOutput(this.Super, alias + 'Environment', {
        value: this.Environment.name,
        exportName: alias + 'Environment',
      });

      new cdk.CfnOutput(this.Super, alias + 'EnvironmentRef', {
        value: this.Environment.ref,
        exportName: alias + 'EnvironmentRef',
      });

      new cdk.CfnOutput(this.Super, alias + 'EnvironmentArn', {
        value: `arn:aws:appconfig:${this.Scope.region}:${this.Scope.account}:application/${this.Super.ref}/environment/${this.Environment.ref}`,
        exportName: alias + 'EnvironmentArn'
      });

      new cdk.CfnOutput(this.Super, alias + 'Profile', {
        value: this.Profile.name,
        exportName: alias + 'Profile',
      });

      new cdk.CfnOutput(this.Super, alias + 'ProfileRef', {
        value: this.Profile.ref,
        exportName: alias + 'ProfileRef',
      });

      new cdk.CfnOutput(this.Super, alias + 'ProfileArn', {
        value: `arn:aws:appconfig:${this.Scope.region}:${this.Scope.account}:application/${this.Super.ref}/configurationprofile/${this.Profile.ref}`,
        exportName: alias + 'ProfileArn'
      });

      return this;
    }

}