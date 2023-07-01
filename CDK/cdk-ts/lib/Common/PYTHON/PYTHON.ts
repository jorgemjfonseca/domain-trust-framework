/* ======================================================
 SETUP 👇
  * install https://docs.docker.com/desktop/install/mac-install/ 
  * npm i -D esbuild -force
  * npm install @aws-cdk/aws-lambda-python-alpha -force
 ======================================================
 INSTRUCTIONS 👇
  * https://medium.com/geekculture/how-to-deploy-a-python-lambda-using-aws-cdk-99479fd28a06
  * https://docs.aws.amazon.com/cdk/api/v2/docs/@aws-cdk_aws-lambda-python-alpha.PythonLayerVersion.html
  * https://docs.aws.amazon.com/cdk/api/v2/docs/aws-lambda-python-alpha-readme.html
====================================================== */

import { PythonFunction, PythonLayerVersion } from '@aws-cdk/aws-lambda-python-alpha'

import { Duration } from 'aws-cdk-lib';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';
import { STACK } from '../STACK/STACK';
import { LAMBDA } from '../LAMBDA/LAMBDA';

// Use only when there's the need for a layer.
export class PYTHON {

    public Super: PythonFunction;

    constructor(sup: PythonFunction) {
        this.Super = sup;
    }

    public static New(scope: STACK, id: string) {

        const baseEntry = path.join(LAMBDA.CallerDirname(), '../lambda/' + id);

        const layer = new PythonLayerVersion(scope, id+'-Layer', {
            layerVersionName: id+'-Layer',
            entry: baseEntry + 'Layer',
            compatibleRuntimes: [
                Runtime.PYTHON_3_7,
                Runtime.PYTHON_3_8,
                Runtime.PYTHON_3_9,
                Runtime.PYTHON_3_10
            ]
        });
        
        const sup = new PythonFunction(scope, id, {
            functionName: scope.Name + '-' + id,
            entry: baseEntry,
            runtime: Runtime.PYTHON_3_10,
            index: 'main.py',
            handler: 'lambda_handler',
            layers: [ layer ],
            timeout: Duration.seconds(10)
        });
        
        return new PYTHON(sup);
    }


    public FunctionName(): string {
        return this.Super.functionName;
    }

}