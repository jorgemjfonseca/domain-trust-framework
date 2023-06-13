#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DomainManifester } from '../lib/DomainManifester/stack/Stack';
import { DomainMessenger } from '../lib/DomainMessenger/_stack/Stack';
import { DomainHost } from '../lib/DomainHost/stack/Stack';
import { DomainSyncAPI } from '../lib/DomainSyncAPI/stack/Stack';

const app = new cdk.App();

new DomainHost(app, {});
new DomainManifester(app, {});
new DomainMessenger(app, {});
new DomainSyncAPI(app, {});


// tsc -w
// isengardcli assume dtfw+authority@amazon.com
// cdk deploy DomainMessenger --require-approval never