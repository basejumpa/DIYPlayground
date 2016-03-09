void setup(){
// Open serial connection.
  Serial.begin(9600);
}
 
void loop(){
  Serial.print("Hello world");
  delay(10); // ms
}
