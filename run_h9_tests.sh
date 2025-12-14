#!/bin/bash
# H9 Test Suite Runner
# Executes all 96 tests with coverage report
# Usage: ./run_h9_tests.sh [--unit|--e2e|--advanced|--contracts|--all]

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║      H9 - Hotel Booking Integration Test Suite Runner          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test files
UNIT_TESTS="src/theaia/tests/unit/services/test_groqtools.py"
E2E_TESTS="src/theaia/tests/integration/test_e2e_booking_flow.py"
ADVANCED_TESTS="src/theaia/tests/integration/test_h09_advanced.py"
CONTRACT_TESTS="src/theaia/tests/integration/test_h09_contracts.py"

# Default to all
TEST_SUITE="${1:-all}"

run_tests() {
    local test_file=$1
    local test_name=$2
    
    echo -e "${BLUE}▶ Running ${test_name}...${NC}"
    echo "────────────────────────────────────────────────────────────────"
    
    if pytest "$test_file" -v --tb=short --color=yes; then
        echo -e "${GREEN}✓ ${test_name} PASSED${NC}"
        return 0
    else
        echo -e "${YELLOW}✗ ${test_name} FAILED${NC}"
        return 1
    fi
}

generate_coverage() {
    echo ""
    echo -e "${BLUE}▶ Generating coverage report...${NC}"
    echo "────────────────────────────────────────────────────────────────"
    pytest \
        $UNIT_TESTS $E2E_TESTS $ADVANCED_TESTS $CONTRACT_TESTS \
        --cov=src/theaia/services/groq_tools \
        --cov-report=html \
        --cov-report=term-missing \
        -q
    echo -e "${GREEN}✓ Coverage report generated: htmlcov/index.html${NC}"
}

case $TEST_SUITE in
    "unit")
        run_tests "$UNIT_TESTS" "Unit Tests (23 tests)"
        ;;
    "e2e")
        run_tests "$E2E_TESTS" "E2E Core Tests (10 tests)"
        ;;
    "advanced")
        run_tests "$ADVANCED_TESTS" "Advanced Tests (35 tests)"
        ;;
    "contracts")
        run_tests "$CONTRACT_TESTS" "Contract Tests (28 tests)"
        ;;
    "all")
        echo -e "${BLUE}Running full H9 test suite (96 tests)${NC}"
        echo ""
        
        run_tests "$UNIT_TESTS" "Unit Tests (23 tests)" || true
        echo ""
        run_tests "$E2E_TESTS" "E2E Core Tests (10 tests)" || true
        echo ""
        run_tests "$ADVANCED_TESTS" "Advanced Tests (35 tests)" || true
        echo ""
        run_tests "$CONTRACT_TESTS" "Contract Tests (28 tests)" || true
        echo ""
        
        # Final summary
        echo -e "${BLUE}▶ Running all tests together for summary...${NC}"
        echo "────────────────────────────────────────────────────────────────"
        if pytest \
            $UNIT_TESTS $E2E_TESTS $ADVANCED_TESTS $CONTRACT_TESTS \
            -v --tb=line --color=yes; then
            echo ""
            echo -e "${GREEN}✓✓✓ ALL 96 TESTS PASSED ✓✓✓${NC}"
            echo ""
            
            # Generate coverage
            generate_coverage
        else
            echo ""
            echo -e "${YELLOW}Some tests failed. Check output above.${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${YELLOW}Unknown test suite: $TEST_SUITE${NC}"
        echo ""
        echo "Usage: ./run_h9_tests.sh [--unit|--e2e|--advanced|--contracts|--all]"
        echo ""
        echo "Examples:"
        echo "  ./run_h9_tests.sh unit              # Run unit tests only"
        echo "  ./run_h9_tests.sh e2e               # Run E2E tests only"
        echo "  ./run_h9_tests.sh advanced          # Run advanced tests only"
        echo "  ./run_h9_tests.sh contracts         # Run contract tests only"
        echo "  ./run_h9_tests.sh all               # Run all tests (default)"
        exit 1
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Test Run Complete!                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
