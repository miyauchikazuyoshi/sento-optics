#!/bin/bash
# Quick progress check for Na production AIMD
LOG="logs/Na_production_md.out"

if [ ! -f "$LOG" ]; then
    echo "No log file found."
    exit 1
fi

NSTEP=$(grep -c "!    total energy" "$LOG" 2>/dev/null || echo 0)
TEMPS=$(grep "temperature" "$LOG" | grep -v "Starting\|controlled" | tail -5)
ENERGY=$(grep "!    total energy" "$LOG" | tail -1)
RUNNING=$(ps aux | grep "pw.x.*Na_production" | grep -v grep | wc -l | tr -d ' ')

echo "========================================"
echo "  Na Liquid AIMD Progress"
echo "========================================"
echo "  Steps completed: $NSTEP / 1200"
echo "  Running: $( [ "$RUNNING" -gt 0 ] && echo "YES ✅" || echo "NO ❌" )"
echo ""
echo "  Last 5 temperatures (K):"
echo "$TEMPS" | awk '{print "    " $NF " K"}'
echo ""
echo "  Latest energy: $ENERGY"
echo ""

if [ "$NSTEP" -gt 0 ]; then
    PCT=$(echo "scale=1; $NSTEP * 100 / 1200" | bc)
    echo "  Progress: ${PCT}%"
    REMAINING=$(echo "scale=0; (1200 - $NSTEP) * 5.2 / 60" | bc)
    echo "  Est. remaining: ~${REMAINING} hours"
fi
echo "========================================"
