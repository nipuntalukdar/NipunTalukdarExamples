package gopipe

type Executor interface {
	Execute(data map[string]interface{}, context interface{})
	AddCollector(Collector)
	AddIdentity(uint)
}
