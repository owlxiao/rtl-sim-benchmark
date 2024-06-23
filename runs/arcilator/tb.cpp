
#define CONCAT_TEMP(a, b) a##b
#define CONCAT(x, y) CONCAT_TEMP(x, y)

#define TO_STR(x) #x
#define HEADER_FILE_NAME(Design) TO_STR(Design.h)

#define dut_eval CONCAT(Design, _eval)

#include HEADER_FILE_NAME(Design)

#include <chrono>
#include <iostream>

int main(int argc, char **argv) {
  auto Dut = Design();
  auto Cycles = std::atoi(argv[1]);

  auto Clock = [&]() {
    Dut.view.clock = false;
    Dut.eval();

    Dut.view.clock = true;
    Dut.eval();
  };

  //===--------------------------------------------------------------------===//
  // Model initialization and reset
  //===--------------------------------------------------------------------===//

  Dut.view.reset = false;

  for (int i = 0; i < 1000; ++i) {
    Dut.view.reset = i < 100;
    Clock();
  }

  //===--------------------------------------------------------------------===//
  // Simulation loop
  //===--------------------------------------------------------------------===//

  auto Start = std::chrono::system_clock::now();

  for (int i = 0; i < Cycles; ++i)
    Clock();

  auto End = std::chrono::system_clock::now();

  std::cout << std::chrono::duration_cast<std::chrono::microseconds>(End -
                                                                     Start)
                   .count()
            << std::endl;

  return 0;
}
