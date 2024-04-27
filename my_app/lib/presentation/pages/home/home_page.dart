import 'package:flutter/material.dart';
import 'package:my_app/presentation/widgets/button_widget.dart';
import 'package:my_app/presentation/widgets/data_widget.dart';
import 'package:my_app/providers/home_provider.dart';
import 'package:my_app/services/mqtt/my_mqtt_client.dart';
import 'package:provider/provider.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with OnMessageArrived {
  late MyMqttClient myMqttClient;

  @override
  void initState() {
    super.initState();
    _connect();
    registerMqttService();
  }

  void _connect() {
    myMqttClient = MyMqttClient(
      "io.adafruit.com",
      "nguyenkhoa2207",
      "aio_TbjA81SH5llj00Eh57ItDj8GDgTT",
    );
  }

  void registerMqttService() {
    myMqttClient.addObserver(this);
  }

  void handleClickLedButton() {
    context.read<HomeProvider>().toggleFan();
    myMqttClient.publish(
        "button1", context.read<HomeProvider>().isFanOn.toString());
  }

  void handleClickPumpButton() {
    context.read<HomeProvider>().togglePump();
    myMqttClient.publish(
        "button2", context.read<HomeProvider>().isPumpOn.toString());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Tracking Farm"),
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20.0),
        child: Column(
          children: [
            DataWidget(
              title: "Temperature",
              value: "${context.watch<HomeProvider>().tempValue}°C",
              color: Colors.red,
              marginTop: 10,
            ),
            DataWidget(
              title: "Humidity",
              value: "${context.watch<HomeProvider>().humidValue}%",
              color: Colors.blue,
              marginTop: 20,
            ),
            DataWidget(
              title: "Light Intensive",
              value: "${context.watch<HomeProvider>().lightValue}%",
              color: Colors.green,
              marginTop: 20,
              marginBottom: 30,
            ),
            Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ButtonWidget(
                    iconColor: Colors.white,
                    backgroundColor:
                        (context.watch<HomeProvider>().isFanOn == 1)
                            ? Colors.amber
                            : Colors.grey.shade400,
                    icon: "ic_lightbulb.png",
                    handleClick: () {
                      handleClickLedButton();
                    },
                  ),
                  ButtonWidget(
                    iconColor: Colors.white,
                    backgroundColor:
                        (context.watch<HomeProvider>().isPumpOn == 1)
                            ? Colors.amber
                            : Colors.grey.shade400,
                    icon: "ic_water_pump.png",
                    handleClick: () {
                      handleClickPumpButton();
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void onArrived(String topic, String payload) {
    if (topic == "sensor1") {
      int value = int.parse(payload);
      context.read<HomeProvider>().setTempValue(value);
    } else if (topic == "sensor2") {
      int value = int.parse(payload);
      context.read<HomeProvider>().setHumidValue(value);
    } else if (topic == "sensor3") {
      int value = int.parse(payload);
      context.read<HomeProvider>().setLightValue(value);
    } else if (topic == "response-button1"){
      int value = int.parse(payload);
      context.read<HomeProvider>().setIsFanOn(value);
    } else if (topic == "response-button2"){
      int value = int.parse(payload);
      context.read<HomeProvider>().setIsPumpOn(value);
    }
  }
}
