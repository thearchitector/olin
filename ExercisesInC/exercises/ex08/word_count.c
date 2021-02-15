#include <stdio.h>
#include <glib.h>

void iterator(char* key, int* value) {
  printf("%s: %i\n", key, *value);
  
  // free the key and values since we don't need them anymore
  //
  // if we intended on using the hash map again, we could specify
  // destroy handlers to clear the keys and values during the
  // table destory. however, since we know we won't, we can
  // delete them now to same time and avoid another O(n) call.
  g_free(key);
  g_free(value);
}

int main(int argc, const char* argv[]) {
  // make sure the command usage is correct
  if(argc != 2) {
    fprintf(stderr, "Invalid command. Try ./word_count <filename>");
    return 1;
  }

  char* contents;
  GError* gerr;

  // read the file contents into the buffers above
  if(!g_file_get_contents(argv[1], &contents, NULL, &gerr)) {
    // if an error occured, print the message and exit with status
    int code = gerr->code;
    fprintf(stderr, "An error was encountered: %s\n", gerr->message);

    // free the error and content string
    g_clear_error(&gerr);
    g_free(contents);
    return code;
  }

  // create a hash table to store the occurances
  GHashTable* hash = g_hash_table_new(g_str_hash, g_str_equal);
  // tokenize the file contents
  char** const words = g_str_tokenize_and_fold(contents, NULL, NULL);
  const int num = g_strv_length(words); 
  int* freq;

  for(int i = 0; i < num; ++i) {
    // get the existing value from the hash table
    freq = g_hash_table_lookup(hash, words[i]);
    // if it exists, increment it
    if(freq != NULL) *freq = *freq + 1;
    else {
      // allocate a new integer set to 1 and add it to the hash table
      freq = malloc(sizeof *freq);
      *freq = 1;
      g_hash_table_insert(hash, words[i], freq);
    }
  }

  // print all the word frequencies
  g_hash_table_foreach(hash, (GHFunc)iterator, NULL);

  // free all the allocated structs
  g_free(contents);
  g_hash_table_destroy(hash);
  return 0;
}
