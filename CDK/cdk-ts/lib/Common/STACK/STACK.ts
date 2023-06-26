import * as cdk from "aws-cdk-lib/core";
import * as ssm from 'aws-cdk-lib/aws-ssm';
import { Construct } from 'constructs';


export class STACK extends cdk.Stack {
    
    public Name: string;

   
    protected constructor(scope: Construct, name: string, props?: cdk.StackProps) {
        super(scope, name, { 
            // 👉 https://github.com/aws-samples/aws-cdk-examples/issues/238
            env: {
                account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT, 
                region: process.env.CDK_DEPLOY_REGION || process.env.CDK_DEFAULT_REGION             
            },
            terminationProtection: true, 
            ...props
        });
        this.Name = name;
    }

    public Count: number = 0;
    public Next(): number {
        this.Count++;
        return this.Count;
    }

    public RandomName(seed?: string): string {
        return (seed??'Random')
            + this.Next()
            //+ (Math.round(Math.random()*1000))
            ;
    }

    private ExportCfn(alias: string, value: string) {
        new cdk.CfnOutput(this, alias, {
            value: value,
            exportName: alias,
        });
    }

    private ExportSsm(alias: string, value: string) {
        new ssm.StringParameter(
            this,
            this.RandomName(alias),
            {
              parameterName: '/dtfw/' + alias,
              stringValue: value, 
              tier: ssm.ParameterTier.ADVANCED,
            },
          );
    }

    public Export(alias: string, value: string): STACK {
        this.ExportCfn(alias, value);
        this.ExportSsm(alias, value);
        return this;
    }

    private ImportCfn(alias: string): string {
        return cdk.Fn.importValue(alias);
    }

    private GetSsm(alias: string): ssm.IStringParameter {
        return ssm.StringParameter
            .fromStringParameterName(this, alias, '/dtfw/' + alias);
    };

    public ImportSsm(alias: string): string {
        return this.GetSsm(alias).stringValue;
    }

   

    public Import(alias: string): string {
        return this.ImportCfn(alias);
        //return this.ImportSsm(alias);
    }

}