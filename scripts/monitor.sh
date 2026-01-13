#!/bin/bash
# Skrypt do monitorowania obciążenia systemu podczas testów

echo "=== MONITOR SYSTEMU ==="
echo "Naciśnij Ctrl+C aby zakończyć"
echo ""

while true; do
    clear
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║         MONITOR OBCIĄŻENIA SYSTEMU - $(date +%H:%M:%S)          ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # CPU
    echo "📊 OBCIĄŻENIE CPU:"
    mpstat 1 1 | grep -A 5 "%idle" | tail -1 | awk '{print "   Użycie: " 100-$NF "%"}'
    echo ""
    
    # Średnie obciążenie
    echo "⚡ LOAD AVERAGE (1min, 5min, 15min):"
    uptime | awk -F'load average:' '{print "   " $2}'
    echo ""
    
    # Pamięć
    echo "💾 PAMIĘĆ:"
    free -h | grep Mem | awk '{print "   Użyte: " $3 " / " $2 " (" int($3/$2*100) "%)"}'
    echo ""
    
    # Procesy pi_calculator
    echo "🔢 PROCESY pi_calculator:"
    pgrep -a pi_calculator | wc -l | awk '{print "   Aktywne procesy: " $1}'
    
    if pgrep pi_calculator > /dev/null; then
        echo ""
        echo "   Szczegóły:"
        ps aux | grep pi_calculator | grep -v grep | awk '{printf "   PID: %-8s CPU: %-6s MEM: %-6s\n", $2, $3"%", $4"%"}'
    fi
    echo ""
    
    # Wątki
    TOTAL_THREADS=$(ps -eLf | grep pi_calculator | grep -v grep | wc -l)
    if [ "$TOTAL_THREADS" -gt 0 ]; then
        echo "🧵 WĄTKI: $TOTAL_THREADS"
        echo ""
    fi
    
    # Czekaj 2 sekundy przed następną aktualizacją
    sleep 2
done
