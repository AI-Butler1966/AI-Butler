#!/bin/bash

PROJECT_DIR="/home/matuura-toshio/AI-Butler"
LOG_RETENTION_DAYS=30

echo ""
echo "=================================================="
echo "🕒 Cron Start: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📁 Project   : $PROJECT_DIR"
echo "=================================================="

cd "$PROJECT_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Cron Result: FAILED"
    echo "Reason: Could not move to project directory."
    echo "🕒 Cron End  : $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=================================================="
    exit 1
fi

mkdir -p logs
echo "🧹 Cleaning old logs..."
DELETED_LOGS=$(find "$PROJECT_DIR/logs" -type f -name "20??-??-??_??-??-??.txt" -mtime +"$LOG_RETENTION_DAYS" -print -delete | wc -l)
echo "🧹 Old Log Cleanup: Deleted $DELETED_LOGS file(s). Retention: ${LOG_RETENTION_DAYS} days"
echo "--------------------------------------------------"

if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Cron Result: FAILED"
    echo "Reason: venv/bin/activate was not found."
    echo "🕒 Cron End  : $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=================================================="
    exit 1
fi

source venv/bin/activate

echo "🚀 Running AI Butler..."
echo "--------------------------------------------------"

python3 main.py

STATUS=$?

echo "--------------------------------------------------"

if [ $STATUS -eq 0 ]; then
    echo "✅ Cron Result: SUCCESS"
else
    echo "❌ Cron Result: FAILED"
    echo "Exit Code: $STATUS"
fi

echo "🕒 Cron End  : $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================="

exit $STATUS
