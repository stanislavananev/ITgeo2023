#define WIFI_SSID "******"
#define WIFI_PASS "******"
#define BOT_TOKEN "******"

#include <FastBot.h>
FastBot bot(BOT_TOKEN);


void connectWiFi() {
  delay(2000);
  Serial.begin(115200);
  Serial.println();

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
    if (millis() > 15000) ESP.restart();
  }
  Serial.println("Connected");
}

void newMsg(FB_msg& msg) {
  // выводим ID чата, имя юзера и текст сообщения
  // Serial.print(msg.chatID);     // ID чата 
  // Serial.print(", ");
  // Serial.print(msg.username);   // логин
  // Serial.print(", ");
  // Serial.println(msg.text);     // текст
  // bot.sendMessage(msg.text, msg.chatID);
  if (msg.text == "Включи свет"){
    bot.sendMessage("Включаю", msg.chatID);
    digitalWrite(LED_BUILTIN, LOW);
    bot.sendMessage("Свет включен", msg.chatID);
  }
  if(msg.text == "Выключи свет"){
    bot.sendMessage("Выключаю", msg.chatID);
    digitalWrite(LED_BUILTIN, HIGH);
    bot.sendMessage("Свет выключен", msg.chatID);
  }  
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  connectWiFi();
  bot.setChatID(1943822081);
  bot.attach(newMsg);
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  bot.tick();
}


