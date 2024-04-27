import 'dart:math';

import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

mixin OnMessageArrived {
  void onArrived(String topic, String payload);
}

class MyMqttClient {
  late MqttClient client;
  final String _serverUri;
  final String? _username;
  final String? _password;
  final String _clientId = _generateClientId();

  List<OnMessageArrived> observers = [];

  MyMqttClient(this._serverUri, this._username, this._password) {
    client = MqttServerClient(
      _serverUri,
      _clientId,
    );
    client.keepAlivePeriod = 30;
    client.logging(on: false);
    client.autoReconnect = true;

    final MqttConnectMessage conMess = MqttConnectMessage()
        .withClientIdentifier(_clientId)
        .withWillTopic("willTopic")
        .withWillMessage("My Will message")
        .startClean();
    client.connectionMessage = conMess;

    client.onConnected = _onConnected;
    client.onSubscribed = _onSubscribed;
    connect();
  }

  static String _generateClientId() {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    final random = Random();
    final clientId = StringBuffer();

    for (var i = 0; i < 16; i++) {
      clientId.write(chars[random.nextInt(chars.length)]);
    }

    return clientId.toString();
  }

  void addObserver(OnMessageArrived observer) {
    observers.add(observer);
  }

  void removeObserver(OnMessageArrived observer) {
    observers.remove(observer);
  }

  void _onConnected() {
    debugPrint('Connected to MQTT broker');

    client.subscribe("$_username/feeds/sensor1", MqttQos.atLeastOnce);
    client.subscribe("$_username/feeds/sensor2", MqttQos.atLeastOnce);
    client.subscribe("$_username/feeds/sensor3", MqttQos.atLeastOnce);
    client.subscribe("$_username/feeds/response-button1", MqttQos.atLeastOnce);
    client.subscribe("$_username/feeds/response-button2", MqttQos.atLeastOnce);
    publish("ping", "1");

    client.updates!
        .listen((List<MqttReceivedMessage<MqttMessage>> messageList) {
      MqttReceivedMessage<MqttMessage> mqttMessage = messageList[0];
      final MqttPublishMessage recMess =
          mqttMessage.payload as MqttPublishMessage;
      try {
        final List<String> parts = mqttMessage.topic.split("/");
        final String topic = parts.last;
        final String payload = MqttPublishPayload.bytesToStringAsString(recMess.payload.message);
        debugPrint('Received message, topic: $topic | payload: $payload');
        for (var observer in observers) {
          observer.onArrived(topic, payload);
        }
      } on Exception catch (e) {
        debugPrint(e.toString());
      }
    });
  }

  void _onSubscribed(String topic) {
    debugPrint("Subsribed topic: $topic");
  }

  void connect() async {
    try {
      debugPrint("Connecting........");
      client.connect(_username, _password);
    } on Exception catch (e) {
      debugPrint("Error: $e");
      debugPrint("Ready to disconnect!");
      client.disconnect();
    }
  }

  void publish(String topic, String payload) {
    final builder = MqttClientPayloadBuilder();
    builder.addString(payload);
    client.publishMessage(
      "$_username/feeds/$topic",
      MqttQos.atLeastOnce,
      builder.payload!,
    );
  }

  void disconnect() {
    debugPrint("Disconnected!");
    client.disconnect();
  }
}
