int incomingByte = 0;
 
void setup(){
// Open serial connection.
Serial.begin(9600);
 
}
 
void loop(){
if (Serial.available() > 0) {
 // read the incoming byte:
 incomingByte = Serial.read();
 
 // say what you got:
 Serial.print("I got: "); // ASCII printable characters
 Serial.println(incomingByte, DEC);
}
 
}
