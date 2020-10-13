import { Fn } from '@aws-cdk/core';

export const PROVIDER_STACK_NAME = 'UniqueValueResource';
export const REGIONAL_STACK_SERVICE_TOKEN = Fn.join('-', [PROVIDER_STACK_NAME, 'ServiceToken']);
