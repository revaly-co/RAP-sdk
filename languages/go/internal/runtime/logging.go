package runtime

import (
	"context"
	"log/slog"
)

// discardHandler is the nil-logger default (the Go analogue of the other
// runtimes' null handlers): a client without a configured Logger emits
// nothing. (slog gained a built-in discard handler after this module's minimum
// Go version.)
type discardHandler struct{}

func (discardHandler) Enabled(context.Context, slog.Level) bool  { return false }
func (discardHandler) Handle(context.Context, slog.Record) error { return nil }
func (d discardHandler) WithAttrs([]slog.Attr) slog.Handler      { return d }
func (d discardHandler) WithGroup(string) slog.Handler           { return d }
