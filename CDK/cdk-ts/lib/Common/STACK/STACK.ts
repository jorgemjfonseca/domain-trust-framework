import * as cdk from "aws-cdk-lib/core";
import * as wafv2 from "aws-cdk-lib/aws-wafv2";
import { Construct } from 'constructs';
import { API } from "../API/API";

export class STACK extends cdk.Stack {
    
    public Name: string;

    constructor(scope: Construct, name: string, props?: cdk.StackProps) {
        super(scope, name, { 
            // 👉 https://github.com/aws-samples/aws-cdk-examples/issues/238
            env: {
                account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT, 
                region: process.env.CDK_DEPLOY_REGION || process.env.CDK_DEFAULT_REGION             
            },
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

    public Export(alias: string, value: string): STACK {
        new cdk.CfnOutput(this, alias, {
            value: value,
            exportName: alias,
        });
        return this;
    }

    public Import(alias: string): string {
        return cdk.Fn.importValue(alias);
    }

}