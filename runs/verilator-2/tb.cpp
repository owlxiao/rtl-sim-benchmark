#define TO_STR(x) #x
#define HEADER_FILE_NAME(Design) TO_STR(Design.h)

#include HEADER_FILE_NAME(Design)

#include <chrono>
#include <iostream>

int main(int argc, char **argv) {
  auto Dut = std::make_unique<Design>();
  auto Cycles = std::atoi(argv[1]);

  auto Clock = [&]() {
    Dut->clock = false;
    Dut->eval();

    Dut->clock = true;
    Dut->eval();
  };

  //===--------------------------------------------------------------------===//
  // Model initialization and reset
  //===--------------------------------------------------------------------===//

  Dut->reset = false;

  for (int i = 0; i < 1000; ++i) {
    Dut->reset = i < 100;
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
