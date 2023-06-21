#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ManifesterBehaviour } from '../lib/Behaviours/Manifester/stack/ManifesterBehaviour';
import { MessengerBehaviour } from '../lib/Behaviours/Messenger/stack/MessengerBehaviour';
import { HostBehaviour } from '../lib/Behaviours/Host/stack/HostBehaviour';
import { SyncApiBehaviour } from '../lib/Behaviours/SyncApi/stack/SyncApiBehaviour';
import { SharedComms } from '../lib/Behaviours/SharedComms/stack/SharedComms';
import { SharedDns } from '../lib/Behaviours/SharedDns/stack/SharedDns';
import { PublisherBehaviour } from '../lib/Behaviours/Publisher/stack/PublisherBehaviour';
import { SubscriberBehaviour } from '../lib/Behaviours/Subscriber/stack/SubscriberBehaviour';
import { ListenerActor } from '../lib/Actors/Backbone/Listener/stack/ListenerActor';
import { GraphActor } from '../lib/Actors/Backbone/Graph/stack/GraphActor';
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

const app = new cdk.App();

// Behaviours
new SharedComms(app, {});
new MessengerBehaviour(app, {});
new SyncApiBehaviour(app, {});
new ManifesterBehaviour(app, {});
new PublisherBehaviour(app, {});
new SubscriberBehaviour(app, {});
new HostBehaviour(app, {});

new SharedDns(app, {});

// Actors/Backbone
new GraphActor(app, {});
new ListenerActor(app, {});

// Actors/Market
new AuthorityActor(app, {});
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
new VaultActor(app, {});

// Devices
new CellTriggerActor(app, {});
new PalmistActor(app, {});
new WiFiActor(app, {});