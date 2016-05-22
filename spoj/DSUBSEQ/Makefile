CXX = g++
OPTS = 
CXXFLAGS = -std=c++11
ALL = DSUBSEQ

all: $(ALL)

$(NAME): $(NAME).o
	$(CXX) -o $(NAME) $(NAME).o $(OPTS)

$(NAME).o: $(NAME).cpp
	$(CXX) -c $(NAME).cpp $(OPTS)

clean:
	rm -rf *o .*o $(ALL)

