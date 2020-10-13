#!/usr/bin/env node
import { App } from '@aws-cdk/core';

import { PROVIDER_STACK_NAME } from '../lib/api';
import { DiagnosticStack } from '../lib/diagnostic-stack';
import { ProviderStack } from '../lib/provider-stack';
import { TestResourcesStack } from '../lib/test-resources-stack';

const app = new App();

// Regional installation
new ProviderStack(app, PROVIDER_STACK_NAME);
// Regional test stack
new TestResourcesStack(app, `${PROVIDER_STACK_NAME}-TestResources`);
// Diagnostic
new DiagnosticStack(app, `${PROVIDER_STACK_NAME}-Diagnostic`);
