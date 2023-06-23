import * as cdk from "aws-cdk-lib/core";
import * as wafv2 from "aws-cdk-lib/aws-wafv2";
import { Construct } from 'constructs';
import { API } from "../API/API";
import { CONSTRUCT } from "../CONSTRUCT/CONSTRUCT";
import { STACK } from "../STACK/STACK";

export class WAF extends CONSTRUCT {

    Super: wafv2.CfnWebACL;
    
    constructor(scope: STACK) {
        super(scope);
    }

    private New() {}

    public static New(scope: STACK, id: string): WAF {
        const ret = new WAF(scope);

        ret.Super = new wafv2.CfnWebACL(scope, `${scope.Name}-${id}`, {
            defaultAction: { allow: {} },
            visibilityConfig: {
                cloudWatchMetricsEnabled: true,
                metricName: 'foo-waf',
                sampledRequestsEnabled: false,
              },
            scope: 'REGIONAL',
            name: `${scope.Name}-${id}`,
            rules: awsManagedRules.map(wafRule => wafRule.rule),
        });

        return ret;
    }

    //https://gist.github.com/statik/f1ac9d6227d98d30c7a7cec0c83f4e64
    AssociateApi(api: API) {
        new WebACLAssociation(this.Super, api.Super.restApiName + "Association", {
            resourceArn: api.Arn(),
            webAclArn: this.Super.attrArn,
        });
    }

}

export class WebACLAssociation extends wafv2.CfnWebACLAssociation {
    constructor(scope: Construct, id: string, props: wafv2.CfnWebACLAssociationProps) {
        super(scope, id,{
            resourceArn: props.resourceArn,
            webAclArn: props.webAclArn,
        });
    }
}



interface WafRule {
    name: string;
    rule: wafv2.CfnWebACL.RuleProperty;
}

const awsManagedRules: WafRule[] = [
    // AWS IP Reputation list includes known malicious actors/bots and is regularly updated
    {
        name: 'AWS-AWSManagedRulesAmazonIpReputationList',
        rule: {
        name: 'AWS-AWSManagedRulesAmazonIpReputationList',
        priority: 10,
        statement: {
            managedRuleGroupStatement: {
            vendorName: 'AWS',
            name: 'AWSManagedRulesAmazonIpReputationList',
            },
        },
        overrideAction: {
            none: {},
        },
        visibilityConfig: {
            sampledRequestsEnabled: true,
            cloudWatchMetricsEnabled: true,
            metricName: 'AWSManagedRulesAmazonIpReputationList',
        },
        },
    },
    // Common Rule Set aligns with major portions of OWASP Core Rule Set
    {
        name: 'AWS-AWSManagedRulesCommonRuleSet',
        rule:
        {
        name: 'AWS-AWSManagedRulesCommonRuleSet',
        priority: 20,
        statement: {
            managedRuleGroupStatement: {
            vendorName: 'AWS',
            name: 'AWSManagedRulesCommonRuleSet',
            // Excluding generic RFI body rule for sns notifications
            // https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-list.html
              excludedRules: [
               { name: 'GenericRFI_BODY' },
               { name: 'SizeRestrictions_BODY' },
            ],
            },
        },
        overrideAction: {
            none: {},
        },
        visibilityConfig: {
            sampledRequestsEnabled: true,
            cloudWatchMetricsEnabled: true,
            metricName: 'AWS-AWSManagedRulesCommonRuleSet',
        },
        },
    },
    // Blocks common SQL Injection
    {
        name: 'AWSManagedRulesSQLiRuleSet',
        rule: {
        name: 'AWSManagedRulesSQLiRuleSet',
        priority: 30,
        visibilityConfig: {
            sampledRequestsEnabled: true,
            cloudWatchMetricsEnabled: true,
            metricName: 'AWSManagedRulesSQLiRuleSet',
        },
        overrideAction: {
            none: {},
        },
        statement: {
            managedRuleGroupStatement: {
            vendorName: 'AWS',
            name: 'AWSManagedRulesSQLiRuleSet',
            excludedRules: [],
            },
        },
        },
    },
    // Blocks common PHP attacks such as using high risk variables and methods in the body or queries
    {
        name: 'AWSManagedRulePHP',
        rule: {
        name: 'AWSManagedRulePHP',
        priority: 40,
        visibilityConfig: {
            sampledRequestsEnabled: true,
            cloudWatchMetricsEnabled: true,
            metricName: 'AWSManagedRulePHP',
        },
        overrideAction: {
            none: {},
        },
        statement: {
            managedRuleGroupStatement: {
            vendorName: 'AWS',
            name: 'AWSManagedRulesPHPRuleSet',
            excludedRules: [],
            },
        },
        },
    },
    // Blocks attacks targeting LFI(Local File Injection) for linux systems
    {
        name: 'AWSManagedRuleLinux',
        rule: {
        name: 'AWSManagedRuleLinux',
        priority: 50,
        visibilityConfig: {
            sampledRequestsEnabled: true,
            cloudWatchMetricsEnabled: true,
            metricName: 'AWSManagedRuleLinux',
        },
        overrideAction: {
            none: {},
        },
        statement: {
            managedRuleGroupStatement: {
            vendorName: 'AWS',
            name: 'AWSManagedRulesLinuxRuleSet',
            excludedRules: [],
            },
        },
        },
    },
];