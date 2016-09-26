# Distiller
 A distributed computing framwork

### About
 Note: _This is still under development._

 This excutes a python program and distributing any computation task (as requeted by the program) among multiple systems.

 It's in two parts.
  - Main system (server): It evaluated the main program, manages the client and also handles code and data distribution.
  - Remote systems (clients): They register themseleves with the server, computes result and return to the server.
