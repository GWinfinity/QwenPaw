/** Per-model (has provider_id, model) or per-date (no provider_id, model) stats. */
export interface TokenUsageStats {
  provider_id?: string;
  model?: string;
  prompt_tokens: number;
  completion_tokens: number;
  call_count: number;
  cost_usd: number;
  cost_cny: number;
}

export interface TokenUsageSummary {
  total_prompt_tokens: number;
  total_completion_tokens: number;
  total_calls: number;
  total_cost_usd: number;
  total_cost_cny: number;
  by_model: Record<string, TokenUsageStats>;
  by_date: Record<string, TokenUsageStats>;
}
