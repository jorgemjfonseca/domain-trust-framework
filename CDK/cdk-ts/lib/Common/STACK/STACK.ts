import * as cdk from "aws-cdk-lib/core";
import * as wafv2 from "aws-cdk-lib/aws-wafv2";
import { Construct } from 'constructs';
import { API } from "../API/API";

export class STACK extends cdk.Stack {
    
    public Name: string;

    constructor(scope: Construct, name: string, props?: cdk.StackProps) {
        super(scope, name, props);
        this.Name = name;
    }

    public Count: number = 0;
    public Next(): number {
        this.Count++;
        return this.Count;
    }

}