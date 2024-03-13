#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <immintrin.h>
#include "./options.h"

int myFunc(int argc, char** argv, bool* vali, long long* n_bytes, struct options* options) {

  *vali = false;
  int option;
  int errFlag = 0;
  options->x = false;
  options->bsize = -1;
  options->in = "none";

  while ((option = getopt(argc, argv, ":i:o:")) != -1) {
    //switch statement to decide which case we use
    switch(option) {
       case 'o':
        if (argc != 6 && argc != 4) {
          errFlag = 3;
          break;
        }

        if (strcmp("stdio", optarg) != 0) {
          options->x = true;
          options->bsize = atoi(optarg);
        }

        if (strcmp("stdio", optarg) != 0 && (strcmp("0", optarg) != 0 && atoi(optarg) < 1)) {
          errFlag = 3;
          break;
        }

        *vali = true;
        break;
      




    case 'i':
        if (argc != 6 && argc != 4) {
          errFlag = 2;
          break;
        }

        if (strcmp("rdrand", optarg) == 0){
          options->in = "rdrand";
        }
        else if (strcmp("mrand48_r", optarg) == 0){
          options->in = "mrand48_r";
        }
        else if ('/' == optarg[0])
	  {
          options->in = "/f";
          options->s = optarg;
        }
        else {
          errFlag = 2;
          break;
        }
        
        *vali = true;
        break;
      
      
      case ':':       
        fprintf(stderr, "Option -%c requires an operand\n", optopt);
        if (optopt == 'i') errFlag = 2;
        else errFlag = 3;
        break;
      
      case '?':
        fprintf(stderr, "Unrecognized option: '-%c'\n", optopt);
        break;
        
      default:
        break;
    }
  }

  if (optind >= argc) {
    return errFlag;
  }

  *n_bytes = atol(argv[optind]);
  if (*n_bytes > 0) {
    if (!errFlag) {
      *vali = true;
    }
  }

  return errFlag;
}
