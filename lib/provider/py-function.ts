import * as lambda from '@aws-cdk/aws-lambda';
import { AssetHashType, BundlingDockerImage, Construct } from '@aws-cdk/core';
import * as path from 'path';

/** Root directory for the python code */
const CODE_PATH = path.join(__dirname, '..', '..');

export interface PyFunctionProps extends lambda.FunctionOptions {
  handler: string;
}

export class PyFunction extends lambda.Function {
  constructor(scope: Construct, id: string, props: PyFunctionProps) {
    const image = BundlingDockerImage.fromAsset(CODE_PATH);

    const functionCode = lambda.Code.fromAsset(CODE_PATH, {
      assetHashType: AssetHashType.OUTPUT,
      bundling: {
        image: image,
        command: ['sh', '-c', 'cp -r /var/task.function/. /asset-output/'],
      },
    });

    const layerCode = lambda.Code.fromAsset(CODE_PATH, {
      assetHashType: AssetHashType.OUTPUT,
      bundling: {
        image: image,
        command: ['sh', '-c', 'cp -r /var/task.layer/. /asset-output/'],
      },
    });

    super(scope, id, {
      ...props,
      runtime: lambda.Runtime.PYTHON_3_8,
      code: functionCode,
    });

    this.addLayers(
      new lambda.LayerVersion(this, 'Deps', {
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_8],
        code: layerCode,
      }),
    );
  }
}
