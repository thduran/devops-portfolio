package main

import "testing"

// checks if basic math is correct
func TestSimpleAssertion(t *testing.T) {
	// 1 + 1 should be equal to 2
	if 1 + 1 != 2 {
		t.Errorf("Sanity check failed: 1 + 1 is not equal to 2")
	}
}