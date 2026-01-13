#!/bin/bash
# Pojedyncze sprawdzenie obciążenia

echo "=== SNAPSHOT OBCIĄŻENIA SYSTEMU ==="
echo ""
echo "🕐 Czas: $(date)"
echo ""

echo "📊 CPU:"
top -bn1 | grep "Cpu(s)" | awk '{print "   Użycie: " $2 " (user) + " $4 " (system)"}'
echo ""

echo "⚡ Load Average:"
uptime | awk -F'load average:' '{print "   " $2}'
echo ""

echo "💾 Pamięć:"
free -h | grep Mem | awk '{print "   Użyte: " $3 " / " $2}'
echo ""

echo "🔢 Procesy pi_calculator:"
COUNT=$(pgrep pi_calculator | wc -l)
echo "   Aktywne: $COUNT"

if [ "$COUNT" -gt 0 ]; then
    echo ""
    echo "   Szczegóły procesów:"
    ps aux | head -1
    ps aux | grep pi_calculator | grep -v grep
fi
echo ""

echo "🧵 Liczba wszystkich wątków:"
ps -eLf | wc -l | awk '{print "   " $1 " wątków"}'
