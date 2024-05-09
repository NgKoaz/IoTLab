import 'package:flutter/material.dart';

class HomeProvider extends ChangeNotifier {
  int tempValue;
  int humidValue;
  int lightValue;

  int isFanOn;
  int isPumpOn;
  int isAuto;

  HomeProvider({
    this.isFanOn = 0,
    this.isPumpOn = 0,
    this.isAuto = 0,
    this.tempValue = 0,
    this.humidValue = 0,
    this.lightValue = 0,
  });

  void setIsFanOn(int isFanOn) {
    this.isFanOn = isFanOn;
    notifyListeners();
  }

  void setIsPumpOn(int isPumpOn) {
    this.isPumpOn = isPumpOn;
    notifyListeners();
  }

  void setTempValue(int value) {
    tempValue = value;
    notifyListeners();
  }

  void setHumidValue(int value) {
    humidValue = value;
    notifyListeners();
  }

  void setLightValue(int value) {
    lightValue = value;
    notifyListeners();
  }

  void toggleFan() {
    isFanOn = (isFanOn == 0) ? 1 : 0;
  }

  void togglePump() {
    isPumpOn = (isPumpOn == 0) ? 1 : 0;
  }

  void toggleAuto() {
    isAuto = (isAuto == 0) ? 1 : 0;
  }

  void setAuto(int value) {
    isAuto = value;
    notifyListeners();
  }
}
