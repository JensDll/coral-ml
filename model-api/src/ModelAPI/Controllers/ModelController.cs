using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Application.Data.Repositories;
using Contracts;
using Contracts.Request;
using Contracts.Response;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace ModelAPI.Controllers
{
    [ApiController]
    public class ModelController : ControllerBase
    {
        private readonly IModelRepository _modelRepository;

        public ModelController(IModelRepository modelRepository)
        {
            _modelRepository = modelRepository;
        }

        [HttpGet(ApiRoutes.Model.GetAll)]
        [ProducesResponseType(typeof(EnumerableEnvelopeDto<TFLiteModelGetAllDto>), StatusCodes.Status200OK)]
        public async Task<IActionResult> GetAll([FromQuery] PaginationRequestDto paginationRequest)
        {
            var models = await _modelRepository.GetAllAsync(paginationRequest);
            Thread.Sleep(2000);
            return Ok(models);
        }

        [HttpGet(ApiRoutes.Model.GetById)]
        public async Task<IActionResult> GetById(int id)
        {
            var model = await _modelRepository.GetByIdAsync(id);

            if (model == null)
            {
                return NotFound();
            }

            return File(model, "application/octet-stream");
        }

        [HttpPost(ApiRoutes.Model.Create)]
        [ProducesResponseType(StatusCodes.Status201Created)]
        public async Task<IActionResult> SaveModel(IFormFile model)
        {
            int id = await _modelRepository.CreateAsync(model);

            return CreatedAtAction(nameof(GetById), new { id }, null);
        }

        [HttpDelete(ApiRoutes.Model.Delete)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        public async Task<IActionResult> Delete(int id)
        {
            await _modelRepository.DeleteAsync(id);

            return NoContent();
        }
    }
}
