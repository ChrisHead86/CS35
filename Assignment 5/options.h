#ifndef OPTIONS
#define OPTIONS

struct options{
  char* s;
  bool x;
  unsigned int bsize;
  char* in;
};

int
myFunc(int argc, char** argv, bool* valid_args, long long* n_bytes, struct options* options);

#endif
