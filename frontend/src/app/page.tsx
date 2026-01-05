export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-4">
          Financial Intelligence System
        </h1>
        <p className="text-lg text-gray-600">
          女性起業家向け金融インテリジェンス配信システム
        </p>
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-6 border rounded-lg">
            <h2 className="text-xl font-semibold mb-2">Twitter監視</h2>
            <p className="text-gray-600">50個のMust Followアカウントをリアルタイム監視</p>
          </div>
          <div className="p-6 border rounded-lg">
            <h2 className="text-xl font-semibold mb-2">AI分析</h2>
            <p className="text-gray-600">Claude Codeによるインテリジェント分析</p>
          </div>
          <div className="p-6 border rounded-lg">
            <h2 className="text-xl font-semibold mb-2">市場データ</h2>
            <p className="text-gray-600">時価総額TOP10リアルタイム追跡</p>
          </div>
          <div className="p-6 border rounded-lg">
            <h2 className="text-xl font-semibold mb-2">配信</h2>
            <p className="text-gray-600">LINE/メールで即時通知</p>
          </div>
        </div>
      </div>
    </main>
  )
}
