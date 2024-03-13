
/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */


#include "./rand64-hw.h"
#include "./rand64-sw.h"
#include "./output.h"
#include "./options.h"
#include "./extra.h"
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <stdio.h>

/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  /* Check arguments.  */
  bool valid = false;
  long long numBytes;
  struct options options;


  //we use the myFunc function to see which errors occur, if any
  int test = myFunc(argc, argv, &valid, &numBytes, &options);

  // If there was an error, display the correct error message
  if (!valid)
    {
      if (test == 2) {
	fprintf(stderr, "%s: usage: %s -i <rdrand/mrand48_r/FILE> NBYTES\n", argv[0], argv[0]);
      }
      else if (test == 3) {
	fprintf(stderr, "%s: usage: %s -o <stdio/N> NBYTES\n", argv[0], argv[0]);
      }
      else {
      fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
      }
      return 1;
    }

  /* If there's no work to do, don't worry about which library to use.  */
  if (numBytes == 0)
    return 0;

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);

  // Take user input and use to decide which random number generator
  if (rdrand_supported() && strcmp("/f", options.in) != 0) {
    if (strcmp("mrand48_r", options.in) == 0) {
          initialize = mrand48r_init;
	  rand64 = mrand48r;
	  finalize = mrand48r_fini;
    }
    else {
      initialize = hardware_rand64_init;
      rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
    }
  }
  else {
    if (strcmp("/f", options.in) == 0) sw_rand64_file(options.s);
    else if (strcmp("rdrand", options.in) == 0) {
      fprintf(stderr, "RDRAND not supported\n");
      return 1;
    }
    initialize = software_rand64_init;
    rand64 = software_rand64;
    finalize = software_rand64_fini;
  }

  initialize ();
  int wordsize = sizeof rand64 ();
  int output_errno = 0;
  int outbytes;
  unsigned long long x = rand64 ();

  // -i case
  if (options.x) {
    if (options.bsize == 0) {
      return 0;
    }

    
    char* buffer = malloc(options.bsize);
    if (buffer == NULL) {
      fprintf(stderr, "Null memory");
      return 1;
    } do {
    outbytes = numBytes < options.bsize ? numBytes : options.bsize;
    
    for (int i = 0; i < outbytes; i++) {
      x = rand64();
      buffer[i] = x;
    }
    
    write(1, buffer, outbytes);
    numBytes -= outbytes;
    }while (0 < numBytes);
    free(buffer);
  }
  else {
   do
    {
      outbytes = numBytes < wordsize ? numBytes : wordsize;
      if (!writebytes (x, outbytes))
	{
	  output_errno = errno;
	  break;
	}
      numBytes -= outbytes;
    }
  while (0 < numBytes);
   }
  
  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }
  
  finalize ();
  return !!output_errno;
}
