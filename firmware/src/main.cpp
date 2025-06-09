#include <Arduino.h>
#include "SX126x.h"
#include "pins.h"

static const uint32_t freq_tx = 915'000'000UL;

SX126x rf;

static char gps_buf[256];

void setup() {
    pinMode(P_LED, OUTPUT);
    pinMode(P_GPS_1PPS, INPUT);
    pinMode(P_GPS_nRST, OUTPUT);

    SPI.setMISO(P_MISO);
    SPI.setMOSI(P_MOSI);
    SPI.setSCLK(P_SCK);
    
    rf.begin(P_RF_CS, P_RF_nRST, P_RF_BUSY);
    rf.setXtalCap(12, 12);
    rf.setFrequency(freq_tx);
    // Note: I don't think this TX power is actually what's going out - it does
    // some duty-cycle-tweaking weirdness instead of setting the direct power
    rf.setTxPower(22, SX126X_TX_POWER_LLCC68);
    rf.setLoRaModulation(7, 125000, 5);
    rf.setLoRaPacket(SX126X_HEADER_EXPLICIT, 12, 15, false);
    rf.setSyncWord(0x3444);

    Serial.setTx(PA2);
    Serial.setRx(PA3);
    Serial.begin(9600);

    digitalWrite(P_LED, LOW);

    digitalWrite(P_GPS_nRST, LOW);
    delay(100);
    digitalWrite(P_GPS_nRST, HIGH);
}

void loop() {
    size_t pktlen = Serial.readBytesUntil('\n', gps_buf, 256);

    if(strncmp(gps_buf, "$GPGGA", strlen("$GPGGA")) == 0) {
        digitalWrite(P_LED, HIGH);
        rf.beginPacket();
        rf.write(gps_buf, pktlen);
        rf.endPacket();
        rf.wait();
        digitalWrite(P_LED, LOW);      
    }
}
