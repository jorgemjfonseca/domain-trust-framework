#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { Manifester } from '../lib/Behaviours/Manifester/stack/ManifesterBehaviour';
import { Messenger } from '../lib/Behaviours/Messenger/stack/MessengerBehaviour';
import { HostBehaviour as Host } from '../lib/Behaviours/Host/stack/HostBehaviour';
import { SyncApi } from '../lib/Behaviours/SyncApi/stack/SyncApi';
import { DomainDns } from '../lib/Behaviours/DomainDns/stack/DomainDns';
import { Publisher } from '../lib/Behaviours/Publisher/stack/Publisher';
import { SubscriberBehaviour as Subscriber } from '../lib/Behaviours/Subscriber/stack/SubscriberBehaviour';
import { ListenerActor as Listener } from '../lib/Actors/Backbone/Listener/stack/ListenerActor';
import { Graph } from '../lib/Actors/Backbone/Graph/stack/GraphActor';
import { AuthorityActor } from '../lib/Actors/Market/Authority/stack/AuthorityActor';
import { CollectorActor } from '../lib/Actors/Market/Collector/stack/CollectorActor';
import { ConsumerActor } from '../lib/Actors/Market/Consumer/stack/CollectorActor';
import { ExchangeActor } from '../lib/Actors/Market/Exchange/stack/ExchangeActor';
import { IdentityActor } from '../lib/Actors/Market/Identity/stack/IdentityActor';
import { IssuerActor } from '../lib/Actors/Market/Issuer/stack/IssuerActor';
import { PayerActor } from '../lib/Actors/Market/Payer/stack/PayerActor';
import { PrinterActor } from '../lib/Actors/Market/Printer/stack/PrinterActor';
import { ProfileActor } from '../lib/Actors/Market/Profile/stack/ProfileActor';
import { RecurrentActor } from '../lib/Actors/Market/Recurrent/stack/SellerActor';
import { SellerActor } from '../lib/Actors/Market/Seller/stack/SellerActor';
import { StorageActor } from '../lib/Actors/Market/Storage/stack/StorageActor';
import { VaultActor } from '../lib/Actors/Market/Vault/stack/VaultActor';
import { ThingsActor } from '../lib/Actors/Market/Things/stack/ThingsActor';
import { CellTriggerActor } from '../lib/Actors/Devices/CellTrigger/stack/CellTrigger';
import { PalmistActor } from '../lib/Actors/Devices/Palmist/stack/PalmistActor';
import { WiFiActor } from '../lib/Actors/Devices/WiFi/stack/WiFiActor';
import { GraphDB } from '../lib/Actors/Backbone/GraphDB/stack/GraphDB';
import { SyncApiEndpoint } from '../lib/Behaviours/SyncApiEndpoint/stack/SyncApiEndpoint';
import { SyncApiDkim } from '../lib/Behaviours/SyncApiDkim/stack/SyncApiDkim';
import { SyncApiHandlers } from '../lib/Behaviours/SyncApiHandlers/stack/SyncApiHandlers';
import { DomainName } from '../lib/Behaviours/DomainName/stack/DomainName';
import { Domain } from '../lib/Behaviours/Domain/stack/Domain';


const app = new cdk.App();

// =====================================
// BEHAVIOURS

const domainName = new DomainName(app);

const domainDns = new DomainDns(app);
domainDns.addDependency(domainName);

const syncApiDkim = new SyncApiDkim(app);
syncApiDkim.addDependency(domainDns);

const syncApiHandlers = new SyncApiHandlers(app);
syncApiHandlers.addDependency(syncApiDkim);

const syncApiEndpoint = new SyncApiEndpoint(app);
syncApiEndpoint.addDependency(domainDns);
syncApiEndpoint.addDependency(syncApiHandlers);

const syncApi = new SyncApi(app);
syncApi.addDependency(domainDns);
syncApi.addDependency(syncApiDkim);
syncApi.addDependency(syncApiEndpoint);
syncApi.addDependency(syncApiHandlers);

const messenger = new Messenger(app);
messenger.addDependency(syncApi);

const manifester = new Manifester(app, {});
manifester.addDependency(domainName);
manifester.addDependency(messenger);

const domain = new Domain(app);
domain.addDependency(manifester);
domain.addDependency(syncApi);
domain.addDependency(messenger);

const publisher = new Publisher(app);
publisher.addDependency(domain);

const subscriber = new Subscriber(app);
subscriber.addDependency(domain);

const host = new Host(app);
host.addDependency(domain);

// ===========================
// Actors/Backbone

const listener = new Listener(app);
listener.addDependency(domain);
listener.addDependency(publisher);

const graphDB = new GraphDB(app);

const graph = new Graph(app);
listener.addDependency(domain);
listener.addDependency(subscriber);
listener.addDependency(graphDB);

// ==========================
// Actors/Market

const authority = new AuthorityActor(app);
authority.addDependency(domain);

const vault = new VaultActor(app, {});
vault.addDependency(domain);
vault.addDependency(host);

new CollectorActor(app, {});
new ConsumerActor(app, {});
new ExchangeActor(app, {});
new IdentityActor(app, {});
new IssuerActor(app, {});
new PayerActor(app, {});
new PrinterActor(app, {});
new ProfileActor(app, {});
new RecurrentActor(app, {});
new SellerActor(app, {});
new StorageActor(app, {});
new ThingsActor(app, {});

// Devices
new CellTriggerActor(app, {});
new PalmistActor(app, {});
new WiFiActor(app, {});