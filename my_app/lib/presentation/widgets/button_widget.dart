import 'package:flutter/material.dart';

class ButtonWidget extends StatelessWidget {
  final Color? iconColor;
  final Color? backgroundColor;

  final String icon;

  final VoidCallback handleClick;

  const ButtonWidget({
    super.key,
    required this.iconColor,
    required this.backgroundColor,
    required this.icon,
    required this.handleClick,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(50),
      ),
      child: IconButton(
        onPressed: handleClick,
        iconSize: 100,
        icon: Image.asset(
          'assets/icons/$icon',
          color: iconColor,
        ),
      ),
    );
  }
}
