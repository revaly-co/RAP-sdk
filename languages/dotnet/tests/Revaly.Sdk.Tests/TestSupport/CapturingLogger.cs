using System.Collections.Concurrent;
using Microsoft.Extensions.Logging;

namespace Revaly.Sdk.Tests.TestSupport;

/// <summary>
/// Captures every formatted log line the SDK emits, for the ADR-SDK-020 log-capture
/// assertions (no payload values at default level, full scrubbing at debug).
/// </summary>
public sealed class CapturingLoggerFactory : ILoggerFactory
{
    private readonly LogLevel _minLevel;

    public CapturingLoggerFactory(LogLevel minLevel = LogLevel.Information)
    {
        _minLevel = minLevel;
    }

    public ConcurrentQueue<string> Lines { get; } = new();

    public string AllOutput => string.Join(Environment.NewLine, Lines);

    public ILogger CreateLogger(string categoryName) => new CapturingLogger(this, categoryName, _minLevel);

    public void AddProvider(ILoggerProvider provider)
    {
    }

    public void Dispose()
    {
    }

    private sealed class CapturingLogger : ILogger
    {
        private readonly CapturingLoggerFactory _owner;
        private readonly string _category;
        private readonly LogLevel _minLevel;

        public CapturingLogger(CapturingLoggerFactory owner, string category, LogLevel minLevel)
        {
            _owner = owner;
            _category = category;
            _minLevel = minLevel;
        }

        public IDisposable? BeginScope<TState>(TState state) where TState : notnull => null;

        public bool IsEnabled(LogLevel logLevel) => logLevel >= _minLevel;

        public void Log<TState>(
            LogLevel logLevel, EventId eventId, TState state, Exception? exception,
            Func<TState, Exception?, string> formatter)
        {
            if (!IsEnabled(logLevel))
            {
                return;
            }

            var line = $"[{logLevel}] {_category}: {formatter(state, exception)}";
            if (exception is not null)
            {
                line += $" | exception: {exception}";
            }

            _owner.Lines.Enqueue(line);
        }
    }
}
