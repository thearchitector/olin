#include <stdio.h>

int hello() {
	int a = 3;
	int b = 4;
	int c = a + b;
	// 
	// subq   $16, %rsp
	// movl   $5, -4(%rbp)
	//
	// The assembely above corresponds to the assignment of the x variable. I am not
	// too sure why 16 is removed from the rsp register, but the movl instruction tells
	// the computer to put the number 5 into memory at address -4(%rbp).
	printf("c is %d\n", c);
	return 0;
}

int main() {
	hello();
	return 0;
}
/**
 *
 * 2. Enabling the optimization flag reduces the number of instructions the computer needs to
 *    execute to perform the same task.
 * 3. Altering the printf statement to output `x` increases the number of instructions the
 *    computer has to execute as it seems to need to first push the 5 to memory, then later pull it
 *    again so it has immediate access to it when it attempts to print. With optimization enabled, the
 *    change is much less noticible, as there are not nearly as many instructions and there fewer steps
 *    in order for the stack to be ready to print the value.
 * 4. Unoptimized, both `x` and `y` seem to be treated as independent variables in located at different
 *    places in memory. To add them, the assembely code instructs the computer to do a lot of registry
 *    loading and unloading in order for the stack to be set up so they can be added. When optimized,
 *    it doesn't look like they are treated as separate variables. They're values are already added and
 *    the instruction simply puts 6 at the memory address. As a result, it does not need to juggle memory
 *    addresses and registries to get the same result.
 *  5. Based on the tests above, optimization seems to try and minimize the number of registry operations
 *     and number of CPU instructions. It does that by making assumptions about the code and preprocessing
 *     where it can (adding x+y during compilation rather than making it happen during runtime). It's much
 *     more conservative with which registries it uses and how it uses them, which also helps reduce the
 *     number of instructions. Less instructions, theoretically faster code. However, in making those
 *     assumptions its also probable that the optimization breaks code.
 */ 
