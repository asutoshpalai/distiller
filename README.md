# Distiller
 A distributed computing framework

### About
 Note: _This is still under development._

 This executes a python program and distributes any computation task (as requested by the program) among multiple systems.

 It's in two parts.
  - Main system (server): It evaluated the main program, manages the client and also handles code and data distribution.
  - Remote systems (clients): They register themselves with the server, receive tasks, compute results and return them to the server.
