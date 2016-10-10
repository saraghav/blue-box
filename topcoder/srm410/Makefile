CC=g++
CFLAGS=-I/usr/local/include/eigen3 --std=c++11
OPTS=
NAME=div2_1000

$(NAME): $(NAME).o
	$(CC) -o $(NAME) $(NAME).o $(OPTS) $(CFLAGS)

$(NAME).o: $(NAME).cpp
	$(CC) -c $(NAME).cpp $(CFLAGS)

clean:
	rm -rf *o .*o $(NAME)

