package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
)

type Equation struct {
	Target   int
	Operands []int
}

func ProcessEquation(target, currentSum int, operands []int, idx int, allowConcat bool) int {
	stack := []struct {
		CurrentSum int
		Idx        int
	}{{
		CurrentSum: operands[0],
		Idx:        0,
	}}

	for len(stack) > 0 {
		// Pop the stack
		n := len(stack) - 1
		state := stack[n]
		stack = stack[:n]

		currentSum, idx := state.CurrentSum, state.Idx

		// Base case: Check if we've reached the last operand
		if idx == len(operands)-1 {
			if currentSum == target {
				return target
			}
			continue
		}

		// Addition
		stack = append(stack, struct {
			CurrentSum int
			Idx        int
		}{
			CurrentSum: currentSum + operands[idx+1],
			Idx:        idx + 1,
		})

		// Multiplication
		if currentSum*operands[idx+1] <= target {
			stack = append(stack, struct {
				CurrentSum int
				Idx        int
			}{
				CurrentSum: currentSum * operands[idx+1],
				Idx:        idx + 1,
			})
		}

		// Concatenation (if allowed)
		if allowConcat {
			concatValue := currentSum*(intPow(10, lenInt(operands[idx+1]))) + operands[idx+1]
			if concatValue <= target {
				stack = append(stack, struct {
					CurrentSum int
					Idx        int
				}{
					CurrentSum: concatValue,
					Idx:        idx + 1,
				})
			}
		}
	}

	return 0
}

// IntPow calculates base^exp for integers.
func intPow(base, exp int) int {
	result := 1
	for exp > 0 {
		if exp%2 == 1 {
			result *= base
		}
		base *= base
		exp /= 2
	}
	return result
}

// LenInt calculates the number of digits in an integer.
func lenInt(n int) int {
	count := 0
	for n > 0 {
		count++
		n /= 10
	}
	return count
}

// GetTotal calculates the sum of results for all equations concurrently.
func GetTotal(equations []Equation, allowConcat bool) int {
	var wg sync.WaitGroup
	results := make(chan int, len(equations))

	for _, eq := range equations {
		wg.Add(1)
		go func(equation Equation) {
			defer wg.Done()
			results <- ProcessEquation(equation.Target, equation.Operands[0], equation.Operands, 0, allowConcat)
		}(eq)
	}

	// Wait for all goroutines to finish and close the results channel
	go func() {
		wg.Wait()
		close(results)
	}()

	// Sum up the results
	total := 0
	for result := range results {
		total += result
	}

	return total
}

// ParseInput reads and parses the input file into a slice of Equations.
func ParseInput(filename string) ([]Equation, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var equations []Equation
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.ReplaceAll(scanner.Text(), ":", "")
		parts := strings.Fields(line)

		if len(parts) < 2 {
			continue
		}

		target, _ := strconv.Atoi(parts[0])
		operands := make([]int, len(parts)-1)
		for i, operand := range parts[1:] {
			operands[i], _ = strconv.Atoi(operand)
		}

		equations = append(equations, Equation{Target: target, Operands: operands})
	}

	return equations, scanner.Err()
}

func main() {
	// Parse input file
	equations, err := ParseInput("input.txt")
	if err != nil {
		fmt.Println("Error reading input file:", err)
		return
	}

	// Compute results
	fmt.Println(GetTotal(equations, false)) // Part 1
	fmt.Println(GetTotal(equations, true))  // Part 2
}
