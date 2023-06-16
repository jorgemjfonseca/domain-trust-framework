#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DomainManifester } from '../lib/Behaviours/DomainManifester/stack/DomainManifester';
import { DomainMessenger } from '../lib/Behaviours/DomainMessenger/stack/DomainMessenger';
import { DomainHost } from '../lib/Behaviours/DomainHost/stack/DomainHost';
import { DomainSyncAPI } from '../lib/Behaviours/DomainSyncAPI/stack/DomainSyncAPI';
import { DomainComms } from '../lib/Behaviours/DomainComms/stack/DomainComms';
import { DomainDNS } from '../lib/Behaviours/DomainDNS/stack/DomainDNS';

const app = new cdk.App();

new DomainComms(app, {});
new DomainDNS(app, {});
new DomainMessenger(app, {});
new DomainSyncAPI(app, {});
new DomainManifester(app, {});
new DomainHost(app, {});


// tsc -w
// isengardcli assume dtfw+authority@amazon.com
// cdk deploy DomainComms --require-approval never
// cdk deploy DomainMessenger --require-approval never