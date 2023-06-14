#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DomainManifester } from '../lib/DomainManifester/stack/DomainManifester';
import { DomainMessenger } from '../lib/DomainMessenger/stack/DomainMessenger';
import { DomainHost } from '../lib/DomainHost/stack/DomainHost';
import { DomainSyncAPI } from '../lib/DomainSyncAPI/stack/DomainSyncAPI';
import { DomainComms } from '../lib/DomainComms/stack/DomainComms';

const app = new cdk.App();

new DomainComms(app, {});
new DomainMessenger(app, {});
new DomainSyncAPI(app, {});
new DomainManifester(app, {});
new DomainHost(app, {});


// tsc -w
// isengardcli assume dtfw+authority@amazon.com
// cdk deploy DomainComms --require-approval never
// cdk deploy DomainMessenger --require-approval never