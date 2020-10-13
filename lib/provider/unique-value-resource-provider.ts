import * as ddb from '@aws-cdk/aws-dynamodb';
import * as logs from '@aws-cdk/aws-logs';
import * as cdk from '@aws-cdk/core';
import { Construct } from '@aws-cdk/core';
import * as cr from '@aws-cdk/custom-resources';

import { PROVIDER_STACK_NAME } from '../api';
import { PyFunction } from './py-function';

export interface IUniqueValueResourceProvider {
  readonly serviceToken: string;
}

export class UniqueValueResourceProvider extends Construct implements IUniqueValueResourceProvider {
  public readonly serviceToken: string;

  public static fromRegionalStack(scope: Construct, id: string): IUniqueValueResourceProvider {
    class Import extends cdk.Resource implements IUniqueValueResourceProvider {
      public readonly serviceToken: string;

      constructor(scope: Construct, id: string) {
        super(scope, id);

        this.serviceToken = cdk.Fn.importValue(cdk.Fn.join('-', [PROVIDER_STACK_NAME, 'ServiceToken']));
      }
    }

    return new Import(scope, id);
  }

  constructor(scope: Construct, id: string) {
    super(scope, id);

    const recordsTable = new ddb.Table(this, 'Records', {
      billingMode: ddb.BillingMode.PAY_PER_REQUEST,
      partitionKey: {
        name: 'group',
        type: ddb.AttributeType.STRING,
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const onEvent = new PyFunction(this, 'OnEvent', {
      handler: 'py/resource_event_handler.on_event',
      environment: {
        RECORDS_TABLE: recordsTable.tableName,
        PYNAMODB_CONFIG: '/var/task/py/lambda_pynamodb_config.py',
      },
      timeout: cdk.Duration.minutes(5),
      logRetention: logs.RetentionDays.ONE_DAY,
    });
    recordsTable.grantFullAccess(onEvent);

    const provider = new cr.Provider(this, 'Provider', {
      onEventHandler: onEvent,
      logRetention: logs.RetentionDays.ONE_DAY,
    });

    this.serviceToken = provider.serviceToken;
  }
}
