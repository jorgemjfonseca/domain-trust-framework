import * as appconfig from 'aws-cdk-lib/aws-appconfig';
import { STACK } from '../STACK/STACK';
import { CONSTRUCT } from '../CONSTRUCT/CONSTRUCT';


export class APPCONFIG extends CONSTRUCT {

    Super: appconfig.CfnApplication;


    constructor (scope: STACK, app: appconfig.CfnApplication)
    {
      super(scope);
      this.Super = app;
    }


    public static New(scope: STACK, name: string, object: any): APPCONFIG {
      
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
      const appConfigEnv = new appconfig.CfnEnvironment(
        ret,
        scope.Name+name+"Env",
        {
          applicationId: app.ref,
          name: "Dev",
        }
      );

      // setup config profile
      const appConfigProfile = new appconfig.CfnConfigurationProfile(
        ret,
        scope.Name+name+"Profile",
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
      const configVersion = new appconfig.CfnHostedConfigurationVersion(
        ret,
        "HostedConfigurationVersion",
        {
          applicationId: app.ref,
          configurationProfileId: appConfigProfile.ref,
          content: JSON.stringify(object),
          // https://www.rfc-editor.org/rfc/rfc9110.html#name-content-type
          contentType: "application/json",
        }
      );
      
      // Perform deployment.
      new appconfig.CfnDeployment(ret, "Deployment", {
        applicationId: app.ref,
        configurationProfileId: appConfigProfile.ref,
        configurationVersion: configVersion.ref,
        deploymentStrategyId: immediateDeploymentStrategy.ref,
        environmentId: appConfigEnv.ref,
      });

      return ret;
    }



}