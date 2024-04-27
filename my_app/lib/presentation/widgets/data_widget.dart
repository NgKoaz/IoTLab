import 'package:flutter/material.dart';

class DataWidget extends StatelessWidget {
  // final double? width;
  // final double? height;
  final String title;
  final String value;
  final Color? color;

  final double? marginTop;
  final double? marginBottom;

  const DataWidget({
    super.key,
    required this.title,
    this.value = "0",
    required this.color,
    this.marginTop = 0,
    this.marginBottom = 0,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          height: marginTop,
        ),
        Container(
          width: double.infinity,
          height: 135,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontFamily: "Montserrat-SemiBold",
                    fontSize: 24,
                  ),
                ),
                Text(
                  value,
                  style: const TextStyle(
                    color: Colors.white,
                    fontFamily: "Montserrat-SemiBold",
                    fontSize: 60,
                  ),
                ),
              ],
            ),
          ),
        ),
        SizedBox(
          height: marginBottom,
        ),
      ],
    );
  }
}
