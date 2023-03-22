CROSS = 
CC = $(CROSS)gcc
CXX = $(CROSS)g++
DEBUG = -Os
CFLAGS = $(DEBUG) -Wall -c

SRCS = $(wildcard ./*.cpp)
OBJS = $(patsubst %.cpp, %.o, $(SRCS))


TARGET = out

$(TARGET) : $(OBJS)
	$(CXX) -o $@ $^ -lwiringPi  
	rm -rf $(OBJS)
	
$(OBJS):%.o : %.cpp
	$(CXX) $(CFLAGS) $< -o  $@ 
	
