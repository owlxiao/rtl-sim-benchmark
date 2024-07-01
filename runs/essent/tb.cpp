#define TO_STR(x) #x
#define HEADER_FILE_NAME(Design) TO_STR(Design.h)

#include HEADER_FILE_NAME(Design)

#include <chrono>
#include <iostream>
#include <string>

int main(int argc, char **argv) {
  auto Dut = std::make_unique<Design>();
  auto Cycles = std::atoi(argv[1]);

  //===--------------------------------------------------------------------===//
  // Model initialization and reset
  //===--------------------------------------------------------------------===//

  Dut->reset = UInt<1>(1);
  Dut->eval(false, false, false);

  for (int i = 0; i < 5; ++i)
    Dut->eval(true, false, false);

  Dut->reset = UInt<1>(0);
  Dut->eval(false, false, false);

  //===--------------------------------------------------------------------===//
  // Simulation loop
  //===--------------------------------------------------------------------===//
  auto Start = std::chrono::system_clock::now();

  for (int i = 0; i < Cycles; ++i)
    Dut->eval(true, false, false);

  auto End = std::chrono::system_clock::now();

  std::cout << std::chrono::duration_cast<std::chrono::microseconds>(End -
                                                                     Start)
                   .count()
            << std::endl;

  return 0;
}