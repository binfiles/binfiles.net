addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

/**
 * Respond to the request
 * @param {Request} request
 */
async function handleRequest(request) {
  path = request.url.replace(/^https:\/\/.*?\//gi, "/");
  return await fetch("http://s3.binfiles.net.s3-website-us-east-1.amazonaws.com" + path)
}