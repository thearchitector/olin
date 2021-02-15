#include <stdio.h>
#include <string.h>
#include "minunit.h"
#include "trout/trout.h"
#include "trout/util.h"

static char* test_icmpcode() {
    char* msg = icmpcode_v4(13);
    char* err = "icmpcode test failed: `icmpcode_v4(13)` should return 'communication administratively prohibited by filtering'";
    mu_assert(err, strcmp(msg, "communication administratively prohibited by filtering") == 0);
    return NULL;
}

int main(int argc, char** argv) {
    char* result = test_icmpcode();

	if (result != NULL) {
        printf("%s\n", result);
    } else {
        printf("* ALL TESTS PASSED *\n");
    }

    return result != NULL;
}
