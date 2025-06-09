#ifndef PINS_H
#define PINS_H

#include <Arduino.h>

static const uint8_t P_TX = PA2, P_RX = PA3, P_DBG_TX = PA9, P_DBG_RX = PA10;
static const uint8_t P_MISO = PA6, P_MOSI = PA7, P_SCK = PA5;
static const uint8_t P_RF_CS = PA4, P_RF_nRST = PB0, P_RF_BUSY = PB1;
static const uint8_t P_GPS_1PPS = PA0, P_GPS_nRST = PA8;
static const uint8_t P_FLASH_CS = PA15;
static const uint8_t P_OWI = PB3, P_LED = PC15;

#endif